// Filename - App.js

// Importing modules
import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/current";
import { AppProvider } from "./pages/current/hooks/app-context";
import List from "./pages/current/components/list-view";

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
          path="/iterative_list"
          element={
            <AppProvider>
              <List type="iterative" />
            </AppProvider>
          }
        />
        <Route
          path="/static_list"
          element={
            <AppProvider>
              <List type="static" />
            </AppProvider>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
