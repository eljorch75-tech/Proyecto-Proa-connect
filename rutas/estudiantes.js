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
});