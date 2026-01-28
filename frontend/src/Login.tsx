import React, { useState } from "react";
import { useLogin } from "./hooks/useAuth";
import {Link} from "react-router-dom"
import './Login.css'
function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { mutate, isPending, isError, error } = useLogin();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    mutate(
      { username, password },
      {
        onSuccess: (data) => {
          console.log(data.profile);
          window.location.href = "/"
        },
        onError: (err) => {
          console.log(err);
        },
      }
    );
  };

return (
  <div className="login-container">
    <div className="login-box">
      <h1 className="login-title">Đăng Nhập</h1>
      
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="username">Tên đăng nhập</label>
          <input
            id="username"
            type="text"
            placeholder="Nhập tên đăng nhập"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Mật khẩu</label>
          <input
            id="password"
            type="password"
            placeholder="Nhập mật khẩu"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="form-input"
          />
        </div>

        {isError && (
          <div className="error-message" role="alert">
            {error?.message || "Đăng nhập thất bại"}
          </div>
        )}

        <button 
          type="submit" 
          disabled={isPending}
          className="submit-button"
        >
          {isPending ? "Đang xử lý..." : "Đăng nhập"}
        </button>
      </form>

      <div className="login-footer">
        <Link to="/forgot-password">Quên mật khẩu?</Link>
        <span> | </span>
        <Link to="/signup">Đăng ký</Link>
      </div>
    </div>
  </div>
);
}

export default Login;
