// Filename - App.js

// Importing modules
import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/current";
import { AppProvider } from "./pages/current/hooks/app-context";
import Rubric from "./pages/current/rubric";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <AppProvider>
              <Home />
            </AppProvider>
          }
        />
        <Route
          path="/rubric"
          element={
            <AppProvider>
              <Rubric />
            </AppProvider>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
