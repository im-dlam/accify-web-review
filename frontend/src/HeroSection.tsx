import React from "react";
import "./HeroSection.css";

function HeroSection() {
  return (
    <div className="container-hero">
      <section className="hero-left reveal visible">
        <h1>TÀI KHOẢN MẠNG XÃ HỘI SỐ LƯỢNG LỚN VÀ GIÁ RẺ</h1>
        <p className="lead">Mỗi tài khoản bán ra đều độc quyền và duy nhất (Không chia sẻ). Tất cả tài khoản được tạo trong vòng 1 tiếng và được xác minh liên tục trước khi bán cho khách hàng.</p>
        <ul className="meta-list">
            <li>
                <i className="fa fa-check-circle"></i>
                Dữ liệu đơn hàng tự động xóa sau 24h
                </li>
            <li>
                <i className="fa fa-check-circle"></i>
                Hỗ trợ IMAP/POP/GRAPH
                </li>
        </ul>
      </section>
      <aside className="hero-right reveal visible">
        <div className="promo-card">
            <h3>Thêm nhiều ưu đãi</h3>
            <p>Nhận mức giảm giá lên đến 20% cho các khách hàng thường xuyên.</p>
            <button>Nhận ưu đãi</button>
        </div>
      </aside>
    </div>
  );
}

export default HeroSection;
