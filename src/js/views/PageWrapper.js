import Header from '../components/Header'

function PageWrapper(props) {
    return (
        <div className='page-wrapper'>
            <Header />
            {props.children}
        </div>
    );
}

export default PageWrapper;