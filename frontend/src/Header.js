import 'bootstrap/dist/css/bootstrap.css';
import './Header.css';

import { useHistory } from "react-router-dom";

function Header() {
    const history = useHistory();

    const onClickHeader = (e) => {
        history.push("/");
    }

    return (
        <div className="header" onClick={onClickHeader}>YouChoose</div>
    );
}

export default Header;
