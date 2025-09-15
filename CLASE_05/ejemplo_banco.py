import threading
import time

# Recurso compartido
saldo = 1000
lock = threading.Lock()

def retirar(dinero, nombre):
    global saldo
    for i in range(3):  # Cada hilo intentará retirar 3 veces
        print(f"[{nombre}] Intentando retirar {dinero} (operación {i+1})...")

        # Bloqueo con lock
        with lock:
            print(f"[{nombre}] ✅ Entró a la sección crítica.")

            if saldo >= dinero:
                print(f"[{nombre}] Retirando {dinero}...")
                saldo -= dinero
                time.sleep(1)  # Simula el tiempo de la transacción
                print(f"[{nombre}] ✅ Operación finalizada. Saldo actual: {saldo}")
            else:
                print(f"[{nombre}] ❌ Fondos insuficientes. Saldo actual: {saldo}")

            print(f"[{nombre}] 🚪 Saliendo de la sección crítica.")

        time.sleep(1)  # Pausa para que los hilos se alternen


def main():
    global saldo
    # Creación de hilos
    h1 = threading.Thread(target=retirar, args=(50, "Hilo-1"))
    h2 = threading.Thread(target=retirar, args=(100, "Hilo-2"))

    # Iniciar hilos
    h1.start()
    h2.start()

    # Esperar a que ambos terminen
    h1.join()
    h2.join()

    print("\nTodas las operaciones han finalizado.")
    print(f"Saldo final: {saldo}")


if __name__ == "__main__":
    main()
