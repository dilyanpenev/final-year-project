import { Link } from "react-router-dom";

function HomePage(props) {
    return (
        <div className="home-page">
            <div className="home-page__banner">
                <h1>Colourise your black-and-white photos <br /> with the help of deep learning</h1>
                <Link to="/demo">
                    <div className="home-page__banner__button">
                        <h3>TRY IT</h3>
                    </div>
                </Link>
            </div>
            <div className="home-page__colour-mix-1"></div>
            <div className="home-page__description">
                <h2>What? Who? Why?</h2>
                <p>Hello! :)</p>
                <p>My name is Dilyan Penev and through this website you can find more about my final-year project for my Bachelor degree in Computer Science at The University of Manchester. The topic of my project is "Colourisation of black-and-white photos" and it focuses on the use of convolutional neural networks. All of the work has been done under the supervision of Professor Angelo Cangelosi.</p>
                <p>By exploring this web application, you can learn more about the inspiration behind the project, the concepts and tools used in the development of this project and how the model was trained for solving this computer vision task. In addition, you will get the chance to test out the colourisation performance by uploading a black-and-white photo which the model will bring back to life for you!</p>
            </div>
            <div className="home-page__colour-mix-2"></div>
            <div className="home-page__acknowledgements">
                <h2>Acknowledgements</h2>
                <p>This project follows the "Colorful Image Colorization" method developed by Richard Zhang, Phillip Isola and Alexei A. Efros. Furthermore, it applies the specified by the authors neural network architecture and uses a portion of the code base that has been made available by the authors.</p>
            </div>
            <div className="home-page__colour-mix-3"></div>
        </div>
    );
}

export default HomePage;