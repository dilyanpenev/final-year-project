import { SectionData } from "../../assets/about_section_data";

function AboutPage(props) {

    return (
        <div className="about-page">
            {SectionData.map(section => {
                return AboutPageSection({ key: section.id, title: section.title, description: section.description })
            })}
        </div>
    );
}

function AboutPageSection(props) {
    return (
        <div className={`about-page__section-${props.key}`}>
            <div className="section-text">
                <h2 className="section-text__title">{props.title}</h2>
                <p className="section-text__title">{props.description}</p>
            </div>
            <div className="section-gradient"></div>
        </div>
    );
}

export default AboutPage;