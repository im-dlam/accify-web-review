import React from 'react'
import HeroSection from "./HeroSection";
import Product from "./Product";

function Home() {
  return <>
    {<HeroSection />}
    {<Product />}
  </>
}

export default Home