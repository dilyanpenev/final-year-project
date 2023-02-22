import Header from '../components/Header'
import { Outlet } from 'react-router-dom'

function PageWrapper(props) {
    return (
        <div className='page-wrapper'>
            <Header />
            <Outlet />
        </div>
    );
}

export default PageWrapper;