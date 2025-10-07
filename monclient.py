# from pymodbus.client import ModbusTcpClient
# import time

# SEUIL_OUVERTURE = 250
# SEUIL_FERMETURE = 250
# TEMPERATURE_REGISTER = 0
# VANNE_COIL = 0

# client = ModbusTcpClient('127.0.0.1', port=502)
# client.connect()

# etat_vanne = 0  # vanne initialement fermée
# historique = []

# try:
#     while True:
#         # Lecture de la température
#         result = client.read_holding_registers(TEMPERATURE_REGISTER, 1)
#         if not result.isError():
#             temperature = result.registers[0]
#             historique.append(temperature)
#             print(f"Température lue : {temperature} °C")

#             # Logique TOR
#             if temperature > SEUIL_OUVERTURE:
#                 etat_vanne = 1
#             elif temperature < SEUIL_FERMETURE:
#                 etat_vanne = 0
#             # Sinon, on garde le dernier état

#             # Écriture de l'état de la vanne
#             client.write_coil(VANNE_COIL, etat_vanne)
#             print(f"Vanne {'OUVERTE' if etat_vanne else 'FERMÉE'}")
#         else:
#             print("Erreur de lecture Modbus")

#         time.sleep(2)
# except KeyboardInterrupt:
#     print("Arrêt du client.")
#     print("Historique des températures :", historique)
# finally:
#     client.close()