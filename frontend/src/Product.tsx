import { useState, useEffect } from "react";

// import "./ProductDark.css";
// import "./ProductLight.css";
import "./Product.css";
const products = [
  {
    id: 1,
    icon: "fa-brands fa-facebook",
    name: "Tài khoản Ngâm",
    category: "facebook",
    subtitle: "Tài khoản Tên Việt | Avatar Việt | Có bài đăng | Bao Ngâm | Get được code | Bao back | Hàng iPhone",
    country: "VN",
    countryFull: "Việt Nam",
    time: "3-6 tháng",
    priceText: "1.200đ",
    priceValue: 1200,
    stock: 120,
  },
  {
    id: 2,
    icon: "fa-brands fa-facebook",
    name: "BM50 New",
    category: "BM",
    subtitle: "Tài khoản Tên Việt | ...",
    country: "VN",
    countryFull: "Việt Nam",
    time: "1-12 tháng",
    priceText: "1.200đ",
    priceValue: 1200,
    stock: 0,
  }
];

function formatVND(value: number) {
  return value.toLocaleString("vi-VN") + "vnđ";
}

function Category({selectedFilter, setSelectedFilter}: {selectedFilter: string, setSelectedFilter: (c: string) => void}){
  const category: string[] = ["Tất cả","Facebook", "Mail", "BM" , "Twitter"];
  return <>
    {category.map (e => {
      return <button className={selectedFilter === e? "active": ""} onClick={() => setSelectedFilter(e)}>{e}</button>
    })} 
  </>
}

export default function Product() {
  const [selectedFilter, setSelectedFilter] = useState<string>("Tất cả");

  const filteredProducts = products.filter(
    (item) =>
      selectedFilter === "Tất cả" ||
      (selectedFilter === "Facebook" && item.category === "facebook") ||
      (selectedFilter === "Mail" && item.category === "mail") ||
      (selectedFilter === "BM" && item.category === "BM")
  );

  return (
    <div className="container-section-product">
      <section className="section-product">
        <div>
          <div className="table-head-left">
            <h4>Sản phẩm</h4>
            <div className="filters">
              <Category selectedFilter={selectedFilter} setSelectedFilter={setSelectedFilter}/>
            </div>
          </div>
          <div className="product-list">
            {filteredProducts.map(item => (
              <div className="product-row" key={item.id} id={item.id.toString()}>
                <div className="col name">
                  <div className="icon"><i className={item.icon}></i></div>
                  <div>
                    <div style={{display:"flex",gap:"8px",alignItems:"center"}}>
                      <div className="title">{item.name}</div>
                      {item.category === "hot" && <div className="badge badge-hot">HOT</div>}
                      {item.category === "facebook" && <div className="badge" style={{background:"#1877f2",color:"#fff"}}>FB</div>}
                      {item.category === "BM" && <div className="badge" style={{background:"#1877f2",color:"#fff"}}>FB</div>}
                      {item.category === "x" && <div className="badge" style={{background:"#000000",color:"#fff"}}>X</div>}
                    </div>
                    <div className="subtitle">{item.subtitle || ""}</div>
                  </div>
                </div>
                <div className="col country" title={item.countryFull || ""}>{item.country}</div>
                <div className="col time">{item.time}</div>
                <div className="col price">{item.priceText || formatVND(item.priceValue)}</div>
                <div className="col stock" data-stock={item.stock}>{item.stock}</div>
                <div className="col action">
                  {item.stock > 0 ? (
                    <button className="btn btn-small btn-buy">Mua</button>
                  ) : (
                    <button className="btn btn-small btn-disabled" disabled>Hết</button>
                  )}
                  <button className="btn btn-small btn-detail">Chi tiết</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}