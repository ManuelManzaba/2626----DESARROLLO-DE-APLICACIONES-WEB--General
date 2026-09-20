CREATE DATABASE IF NOT EXISTS ferreteria_db;
USE ferreteria_db;

-- 1. Tabla Proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100)
);

-- 2. Tabla Productos (con Clave Foránea apuntando a Proveedores)
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

-- 3. Tabla Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(15) NOT NULL UNIQUE,
    telefono VARCHAR(15),
    correo VARCHAR(100)
);

-- 4. Tabla Facturas (con Clave Foránea apuntando a Clientes)
CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);