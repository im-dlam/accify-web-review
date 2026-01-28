import React, { useContext, createContext, useState, useEffect, useRef} from "react";
import { Link } from "react-router-dom";
import './Header.css'
import useUser from "./UserInfo";
import { useLogout } from "./hooks/useAuth";

interface ThemeContextType {
    toggle: () => void,
    theme: string
}


const ThemeContext = createContext<ThemeContextType|undefined>(undefined);

export const ThemeProvider: React.FC<{children: React.ReactNode}> = ({children}) => {
    const [theme, setTheme] = useState<string>(() => localStorage.getItem("theme") || "dark");

    useEffect(() => {
        localStorage.setItem("theme", theme);
        document.documentElement.setAttribute('data-theme', theme);
        document.body.className = theme === "dark" ? "dark-theme" : "light-theme";
    }, [theme])

    const toggle = () => setTheme(t => (t === "light" ? "dark" : "light"))
    return <ThemeContext.Provider value={{theme, toggle}}>
        {children}
    </ThemeContext.Provider>
}

export const useTheme = () => {
    const ctx = useContext(ThemeContext);
    if (!ctx) throw new Error("Theme error");
    return ctx;
}

export default function Headers(){
    const {theme, toggle} = useTheme();
    const {user, isLoading} = useUser();
    const {mutate, isPending} = useLogout()
    const [open, setOpen] = useState<boolean>(false);
    const menuRef = useRef<HTMLDivElement>(null);


    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
            setOpen(false);  // Đóng menu nếu click ngoài user-menu
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);
  
    const handleLogout = () => {
        mutate(undefined, {
            onSuccess: () => {
                window.location.href = "/"
            },
            onError: (error) => {
                console.error(`Logout err: ${error}`)
            }
        })
    }

    return (
        <header className="site-header">
            <div className="container header-inner">
                <Link to="/" className="brand">
                    <span className="brand-text">BAN <strong>VIA</strong></span>
                </Link>

                <nav className="nav" aria-label="Chính">
                    <a href="#dashboard">Dashboard</a>
                    <a href="#mailbox">Đọc hộp thư</a>
                    <a href="#api">Tài liệu APIs</a>
                </nav>

                <div className="header-actions">
                    <button 
                        className="btn-head btn-icon" 
                        onClick={toggle}
                        aria-label="Chuyển giao diện"
                        title={theme === "light" ? "Dark mode" : "Light mode"}
                    >
                        {theme === "light" && <i className="fa-solid fa-sun"></i>}
                        {theme === "dark" && <i className="fa-regular fa-moon"></i>}
                    </button>

                    {!user && !isLoading && (
                        <Link to="/login" className="btn-head btn-primary header-cta">
                            Đăng nhập
                        </Link>
                    )}

                    {user && (
                        <div className="user-menu" ref={menuRef}>
                            <Link to="/profile" className="btn-head btn-icon user-btn" title={user} onClick={
                                    e => {
                                        e.preventDefault();
                                        setOpen(!open)
                                        }}>
                                <i className="fa-solid fa-user-circle"></i>
                                <span className="user-name">{user}</span>
                            </Link>
                            {
                                open && (
                                    <div className="user-submenu">
                                        <button 
                                            onClick={handleLogout}
                                            disabled={isPending}
                                            className="btn-small btn-icon btn-logout"
                                            title="Đăng xuất"
                                        >
                                            <i className="fa-solid fa-sign-out-alt"></i>
                                            Đăng xuất
                                        </button>
                                    </div>

                                )
                            }
                        </div>
                    )}
                </div>
            </div>
        </header>
    )
}