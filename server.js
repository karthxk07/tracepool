const express = require('express');
const app = express();
const path = require('path');

app.set("trust proxy", true);


const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

// Create a single supabase client for interacting with your database
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);

app.get("/", async (req, res) => {

  const { error } = await supabase.from("logger").insert([{ ip: String(req.ip) }]);
  if (error) {
    console.log(error);
  }
  res.sendFile(path.join(__dirname, "index.html"));
})

app.get("/rickroll.gif", (_, res) => {
  res.sendFile(path.join(__dirname, "rickroll.gif"));
})


app.listen(3000, () => { "server started on port 3000" });
