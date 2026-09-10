const express = require("express");

const app = express();
const PORT = 3000;

app.use(express.json());

console.log("antes");

app.listen(PORT, async() => {
    console.log(`servidor ejecutándose en http://localhost:${PORT}`);
});
