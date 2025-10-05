import '../App.css'
import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

export function Trash() {
    const [allElements, setTrashElements] = useState([]);
    const [toggleRefresh, setToggle] = useState(false);



    const handleRestoreButtonClick = (collection, element) => {
        if (collection) {
            handleRestoreElement(element.title, "collection",null);
        }
        else {
            handleRestoreElement(element._id, "item", element.collection);
        }
    };
    const handleRestoreElement = (id, tp, destination) => {
        axios.put(`http://localhost:5000/trash/restore-element/${id}/${tp}/${destination}`)
            .then(res => {
                setToggle(!toggleRefresh);
                console.log(res);
            })
            .catch(err => console.log(err))
    }
    const handleDeleteButtonClick = (collection, element) => {
        if (collection) {
            handleDeleteElement(element.title, element.type);
        }
        else {
            handleDeleteElement(element._id, "item");
        }
        
    }

    const handleDeleteAllItems = () => {
        axios.delete("http://localhost:5000/trash/delete-all-items")
            .then(res => {
                setToggle(!toggleRefresh);
                console.log(res);
            })
            .catch(err => console.log(err))
    };

    const handleDeleteElement = (id, tp) => {
        axios.delete(`http://localhost:5000/trash/delete-element/${id}/${tp}`)
            .then(res => {
                setToggle(!toggleRefresh);
                console.log(res);
            })
            .catch(err => console.log(err));
    };

    useEffect(() => {
        axios.get("http://localhost:5000/trash/get-all-elements")
            .then(res => {
                setTrashElements(res.data);
            })
            .catch(err => console.log(err));
    }, [])
    useEffect(() => {
        axios.get("http://localhost:5000/trash/get-all-elements")
            .then(res => {
                setTrashElements(res.data);
            })
            .catch(err => console.log(err));
    }, [toggleRefresh])

    return (
        <>
            <div style={{}}>
                <Link to="/">Home</Link>
                <div style={{ display: 'flex', alignItems: 'left', justifyContent: 'left', position: 'relative' } }>
                    <h1 style={{ right: '100%', center: '10%', position: 'absolute' }}>
                        <ul style={{ borderRadius: '15%'}}>
                            {allElements.map(element => (
                                <li className="dropdown-item" style={{ height: '100px', whiteSpace: 'nowrap', textOverflow: 'ellipsis', marginLeft: '0px', margin: '0px' }} key={element._id ? element._id : element.title}>{element.title}
                                    <p style={{ left: '50px', position: 'relative', fontSize: '25px' }}>{element.type ? element.type : 'item'}</p>
                                    <button style={{ fontSize: '25px', height: '65px', width: '150px', position: 'relative', left: '100px', top: '-10px' }} onClick={() => { element.type ? handleRestoreButtonClick(true, element) : handleRestoreButtonClick(false, element) }}>Restore</button>
                                    <button style={{ fontSize: '25px', height: '65px', width: '150px', position: 'relative', left: '100px', top: '-10px' }} onClick={() => { element.type ? handleDeleteButtonClick(true, element) : handleDeleteButtonClick(false, element) } }>Delete</button>
                                </li>
                                
                            )) }

                        </ul>
                    </h1>
                </div>
                
                    
                

                <button onClick={handleDeleteAllItems}>Delete All Items</button>
            </div>
        </>
    )
}