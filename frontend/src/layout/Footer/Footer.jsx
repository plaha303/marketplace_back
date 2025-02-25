import FooterTop from "../../components/Footer/FooterTop";
import FooterBottom from "../../components/Footer/FooterBottom";


function Footer() {
  return (
    <footer className="bg-[#161616]  py-[40px] text-[#FBFCF3]">
      <div className="container mx-auto px-[15px]">
        <FooterTop/>
        <FooterBottom/>
      </div>
    </footer>
  );
}

export default Footer;