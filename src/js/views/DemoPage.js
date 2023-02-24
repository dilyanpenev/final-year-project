import { useState, useRef } from "react";
import upload_icon from "../../assets/upload-icon.png";

function DemoPage(props) {
    const [selectedFile, setSelectedFile] = useState();
    const [imagePreview, setImagePreview] = useState();
    const [isFileUploaded, setFileUploaded] = useState(false);

    const changeHandler = (event) => {
        setSelectedFile(event.target.files[0]);

        if (event.target.files[0] !== undefined) {
            setFileUploaded(true);
            const reader = new FileReader();
            reader.addEventListener("load", () => {
                setImagePreview(reader.result);
            });
            reader.readAsDataURL(event.target.files[0]);
        }
        else {
            setFileUploaded(false);
        }
    };

    const downloadRef = useRef(null);
    const scrollToDownload = () => downloadRef.current.scrollIntoView({ behavior: "smooth" })

    return (
        <div className="demo-page">
            <div className="demo-page__upload">
                <h2>Colourise your photo</h2>
                <div className="display demo-page__upload__file-select">
                    <div className="file-overlay">
                        <img src={isFileUploaded ? imagePreview : upload_icon} alt="Upload Icon" />
                        <div className="demo-page__upload__file-select__text">
                            <h3>{isFileUploaded ? `You have selected ${selectedFile.name}` : "Click to upload a photo"}</h3>
                        </div>
                    </div>
                    <input className="file-selector" type="file" name="file" onChange={changeHandler} accept="image/png, image/jpeg" />
                </div>
                {isFileUploaded &&
                    <div className="demo-page__upload__controls">
                        <div className="button demo-page__upload__controls__submit"
                            onClick={scrollToDownload}>
                            <h3>COLOURISE</h3>
                        </div>
                        <div className="button demo-page__upload__controls__retry">
                            <h3>choose another photo</h3>
                        </div>
                    </div>
                }
            </div>
            <div ref={downloadRef} className="demo-page__result">
                <div className="display demo-page__result__image"></div>
                <div className="button demo-page__result__download">
                    <h3>DOWNLOAD</h3>
                </div>
            </div>
        </div>
    );
}

export default DemoPage;