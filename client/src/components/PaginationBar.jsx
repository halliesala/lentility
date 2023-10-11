import { Pagination } from 'semantic-ui-react';

export default function PaginationBar({ activePage, setActivePage, totalPages }) {

    function handlePageChange(e) {
        setActivePage(e.target.getAttribute('value'))
    }

    return (
        <Pagination
            onPageChange={handlePageChange}
            totalPages={totalPages}
            activePage={activePage}
        />
    )
}