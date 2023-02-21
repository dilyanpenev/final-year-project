import logo from "../../assets/logo-placeholder.png";

function Header(props) {
    return (
        <div className="header" >
            <div className="header__spiral"></div>
            <div className="header__menubar">
                <div className="header__menubar__logo">
                    <img src={logo} alt="Colourisation logo" />
                </div>
                <div className="header__menubar__navigation">
                    <div className="header__menubar__navigation__button">
                        <h2>Home</h2>
                    </div>
                    <div className="header__menubar__navigation__button">
                        <h2>Demo</h2>
                    </div>
                    <div className="header__menubar__navigation__button">
                        <h2>About</h2>
                    </div>
                </div>
            </div>
        </div >
    );
}

export default Header;