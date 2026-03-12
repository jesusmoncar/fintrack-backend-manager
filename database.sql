CREATE DATABASE IF NOT EXISTS gestor_inversiones;
USE gestor_inversiones;

CREATE TABLE IF NOT EXISTS inversiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad DECIMAL(18, 8) NOT NULL,
    precio_compra DECIMAL(18, 8) NOT NULL,
    fecha_compra DATE NOT NULL,
    inversion_total DECIMAL(18, 2) NOT NULL,
    inversion_neta DECIMAL(18, 2) NOT NULL,
    ajuste_manual DECIMAL(18, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS historial_precios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inversion_id INT NOT NULL,
    fecha DATE NOT NULL,
    precio_actual DECIMAL(18, 8) NOT NULL,
    valor_actual DECIMAL(18, 2) NOT NULL,
    ganancia_perdida DECIMAL(18, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inversion_id) REFERENCES inversiones(id) ON DELETE CASCADE,
    UNIQUE KEY unique_inversion_fecha (inversion_id, fecha)
);
