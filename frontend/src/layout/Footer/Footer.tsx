
import FooterBottom from "@/components/Footer/FooterBottom";
import FooterTop from "@/components/Footer/FooterTop";



function Footer() {
  return (
    <footer className="bg-primary-900  pt-[80px] pb-4 text-[#FBFCF3]">
      <div className="container mx-auto px-[15px]">
        <FooterTop />
        <FooterBottom />
      </div>
    </footer>
  );
}

export default Footer;