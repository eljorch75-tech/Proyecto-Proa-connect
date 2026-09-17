const express = require ("express");
const pool = require("../bd/coexion");

const router = express.Router();

//Agregar un estudiante
router.post("/", async (req, res) => {
    const {
        nombre,
        apellido,
        dni,
        fecha_nacimiento,
        nombre_tutor,
        telefono_tutor,
        email_tutor
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO estudiantes
            (nombre, apellido, dni, fecha_nacimiento, nombre_tutor, telefono_tutor, email_tutor, id_estudiante) VALUES(?, ?, ?, ?, ?, ?, ?, ?)`,
            [
              nombre,
              apellido,
              dni,
              fecha_nacimiento,
              nombre_tutor,
              telefono_tutor,
              email_tutor
            ]
        )
        return res.status(201).json({
            mensaje: "estudiantes agregado correctamente"
        })
    } catch (error) {
        return res.status(500).json({
            error: "No se pudo agregar los estudiantes",
            detalle: error.mensaje
        })
    }
});