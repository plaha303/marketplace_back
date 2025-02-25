import FooterTop from "../../components/Footer/FooterTop";
import FooterBottom from "../../components/Footer/FooterBottom";


function Footer() {
  return (
    <footer className="footer-center bg-[#161616] px-[68px] py-[40px]">
      <div className="container text-[#FBFCF3]">
        <FooterTop/>
        <FooterBottom/>
      </div>
    </footer>
  );
}

export default Footer;