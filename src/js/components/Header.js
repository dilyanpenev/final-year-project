import logo from "../../assets/logo-image.png";
import { Link } from "react-router-dom";

function Header(props) {
    return (
        <div className="header" >
            <div className="header__spiral"></div>
            <div className="header__menubar">
                <div className="header__menubar__logo">
                    <Link to="/">
                        <img src={logo} alt="Colourisation logo" />
                    </Link>
                </div>
                <div className="header__menubar__navigation">
                    <div className="header__menubar__navigation__button">
                        <Link to="/">
                            <h2>Home</h2>
                        </Link>
                    </div>
                    <div className="header__menubar__navigation__button">
                        <Link to="/demo">
                            <h2>Demo</h2>
                        </Link>
                    </div>
                    <div className="header__menubar__navigation__button">
                        <Link to="/about">
                            <h2>About</h2>
                        </Link>
                    </div>
                </div>
            </div>
        </div >
    );
}

export default Header;