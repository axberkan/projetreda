import random
import time
import numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusDeviceContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from threading import Thread

# Adresse du registre où la température sera stockée
TEMPERATURE_REGISTER = 0
STATUS_COIL = 0

def temperature_simulation(context, slave_id=0x00):
    """Simule une variation de température toutes les secondes."""
    temperature = 250  # Température initiale (ex: 20.0°C, multipliée par 10)
    while True:
        status = context[slave_id].getValues(1, STATUS_COIL)[0]
        if status:  # Si le chauffage est en marche
            # Variation aléatoire de la température
            temperature += random.randint(-2, 2)
            if temperature < 240:
                temperature = 240
            if temperature > 260:
                temperature = 260
            # Mise à jour du registre
            context[slave_id].setValues(3, TEMPERATURE_REGISTER, [temperature])

        # Lecture et affichage de la valeur lue par le Modbus
        temp_modbus = context[slave_id].getValues(3, TEMPERATURE_REGISTER)[0]
        print(f"Valeur de température du réacteur : {temp_modbus} °C")


        # Logique TOR : vanne ouverte si température >= 250, fermée sinon
        if temp_modbus >= 250:
            context[slave_id].setValues(1, 1, [True])   # Vanne ouverte
        else:
            context[slave_id].setValues(1, 1, [False])  # Vanne fermée

        vanne_ouverte = context[slave_id].getValues(1, 1)[0]
        print(f"Vanne TOR : {'OUVERTE' if vanne_ouverte else 'FERMÉE'}")
        time.sleep(1)


if __name__ == "__main__":
    # Création du datastore Modbus avec un registre de 10 mots
    device = ModbusDeviceContext(
        co=ModbusSequentialDataBlock(0, [True]*10),    # en marche initialement
        hr=ModbusSequentialDataBlock(0, [200]*10)  # 20.0°C initial
    )
    context = ModbusServerContext(devices=device, single=True)

    # Lancement du thread de simulation de température
    sim_thread = Thread(target=temperature_simulation, args=(context,))
    sim_thread.daemon = True
    sim_thread.start()

    # Affichage graphique en temps réel de la température
    temperatures = []
    def update(frame):
        temp = context[0x00].getValues(3, TEMPERATURE_REGISTER)[0]
        temperatures.append(temp)

        # --- Calcul du débit calorifique pour toutes les températures enregistrées ---
        cp = 4180  # J/kg·K (eau)
        T_eau = 70 # °C (température eau d'entrée)
        debit_massique = 1.0 # kg/s (à adapter selon ton installation)

        # Affiche uniquement la dernière valeur
        t = temperatures[-1]
        Q = debit_massique * cp * (t - T_eau)
        print(f"\n{t:6.1f} °C  <-->  {Q:10.2f} W")

        plt.cla()
        plt.plot(temperatures, label='Température (°C)')
        plt.xlabel('Temps (s)')
        plt.ylabel('Température')
        plt.legend()
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), update, interval=1000)
    print("Serveur Modbus TCP démarré sur le port 502...")
    plt.show()

    # Démarrage du serveur Modbus TCP sur le port 502
    StartTcpServer(context, address=("0.0.0.0", 502))

