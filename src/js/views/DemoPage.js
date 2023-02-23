import { useState } from "react";
import upload_icon from "../../assets/upload-icon.png";

function DemoPage(props) {
    const [isFileUploaded, setFileUploaded] = useState(false);

    return (
        <div className="demo-page">
            <div className="demo-page__upload">
                <h2>Colourise your photo</h2>
                <div className="display demo-page__upload__file-select">
                    <img src={upload_icon} alt="Upload Icon" />
                    <div className="demo-page__upload__file-select__text">
                        <h3>Click to upload a photo</h3>
                    </div>
                </div>
                <div className="demo-page__upload__controls">
                    <div className="button demo-page__upload__controls__submit">
                        <h3>COLOURISE</h3>
                    </div>
                    <div className="button demo-page__upload__controls__retry">
                        <h3>choose another photo</h3>
                    </div>
                </div>
            </div>
            <div className="demo-page__result">
                <div className="display demo-page__result__image"></div>
                <div className="button demo-page__result__download">
                    <h3>DOWNLOAD</h3>
                </div>
            </div>
        </div>
    );
}

export default DemoPage;