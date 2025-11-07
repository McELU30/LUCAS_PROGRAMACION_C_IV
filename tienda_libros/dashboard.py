from conexion import conectar

def mostrar_libros():
    conexion = conectar()
    if not conexion:
        print("⚠️ Error al conectar a la base de datos.")
        return

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()

    print("\n📚 LISTA DE LIBROS 📚")
    print("-" * 80)
    print(f"{'ID':<5} {'Título':<30} {'Autor':<25} {'Precio':<10} {'Stock':<5}")
    print("-" * 80)
    for libro in libros:
        print(f"{libro[0]:<5} {libro[1]:<30} {libro[2]:<25} {libro[4]:<10} {libro[5]:<5}")
    print("-" * 80)

    cursor.close()
    conexion.close()

def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    isbn = input("ISBN: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))

    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        sql = "INSERT INTO libros (Titulo, Autor, ISBN, Precio, Stock) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (titulo, autor, isbn, precio, stock))
        conexion.commit()
        print("✅ Libro agregado correctamente.")
        cursor.close()
        conexion.close()
    else:
        print("⚠️ No se pudo conectar a la base de datos.")

def eliminar_libro():
    id_libro = input("ID del libro a eliminar: ")

    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM libros WHERE LibroID = %s", (id_libro,))
        conexion.commit()
        print("🗑️ Libro eliminado correctamente.")
        cursor.close()
        conexion.close()
    else:
        print("⚠️ No se pudo conectar a la base de datos.")

def dashboard():
    while True:
        print("""
=============================
🏠 DASHBOARD - TIENDA LIBROS
=============================
1. Ver todos los libros
2. Agregar un nuevo libro
3. Eliminar un libro
4. Salir
""")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            mostrar_libros()
        elif opcion == "2":
            agregar_libro()
        elif opcion == "3":
            eliminar_libro()
        elif opcion == "4":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida. Intenta nuevamente.")