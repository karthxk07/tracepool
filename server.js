const express = require('express');
const app = express();
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

// Create a single supabase client for interacting with your database
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);

app.get("/", async (req, res) => {

  const { error } = await supabase.from("logger").insert([{ ip: String(req.ip) }]);

  if (error) {
    console.log(error);
  }

  res.end(req);
})



app.listen(3000, () => { "server started on port 3000" });
