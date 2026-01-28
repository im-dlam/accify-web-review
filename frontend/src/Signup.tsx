import React, { useState} from "react";
import { useRegister } from "./hooks/useAuth";
import "./Signup.css";
import { Link } from "react-router-dom";
function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { mutate, isPending, isError, error } = useRegister();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    mutate(
      { email, username, password },
      {
        onSuccess: (data) => {
          console.log(data);
          window.location.href = "/";
        },
        onError: (err) => {
          console.log(err);
        },
      },
    );
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="login-title">Đăng ký</h1>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input 
              type="text"
              id="email"
              placeholder="Email của bạn" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="form-input"
              />
          </div>

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
              {error?.message || "Đăng ký thất bại"}
            </div>
          )}

          <button type="submit" disabled={isPending} className="submit-button">
            {isPending ? "Đang xử lý..." : "Đăng ký"}
          </button>
        </form>

        <div className="login-footer">
          <Link to="/forgot-password">Quên mật khẩu?</Link>
          <span> | </span>
          <Link to="/login">Đăng nhập</Link>
        </div>
      </div>
    </div>
  );
}

export default Signup;
