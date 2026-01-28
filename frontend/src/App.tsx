import React from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Headers, { ThemeProvider } from "./Header";
import { UserProvider } from "./UserInfo";
import Login from "./Login";
import Signup from "./Signup"
import Home from "./Home";
import { QueryClient, QueryClientProvider} from "@tanstack/react-query";


export const queryClient = new QueryClient();
function AppContent() {
  const location = useLocation();
  const pathnames: any = [];
  // const pathnames = ["/login", "/register"];
  const hideHeader = pathnames.includes(location.pathname);

  return (
    <>
      {!hideHeader && <Headers />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <UserProvider>
          <ThemeProvider>
            <AppContent />
          </ThemeProvider>
        </UserProvider>
      </BrowserRouter>
    </QueryClientProvider>
    </>
  );
}
