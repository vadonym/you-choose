import './Loading.css';

function Loading() {
    return (
        <div className="spinner-border text-warning loading-spinner" role="status">
            <span className="sr-only">Loading...</span>
        </div>
    );
}

export default Loading;
