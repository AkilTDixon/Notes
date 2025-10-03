import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { useMark } from '@/components/tiptap-ui/mark-button'
import { SimpleEditor } from '@/components/tiptap-templates/simple/simple-editor'
import './App.css'


function App() {
    const [title, setTitle] = useState("");
    const [allCollectionNames, setCollections] = useState([]);
    const [currentCollection, setCurrentCollection] = useState("");
    const [allItems, setItems] = useState([{ title: " ", body: " "}]);
    const [itemID, setItemID] = useState("");
    const [editorContent, setEditorContent] = useState({ json: {}, html: "", text: "" });
    const [loadCol, setLoadCollection] = useState(false);
    const [editingTitle, setEditingTitle] = useState(false);
    const [refreshCollections, toggleRefresh] = useState(false);
    const [showRenameInput, setShowRenameInput] = useState(false);

    //Hidden dropdowns
    const [showList, setShowList] = useState(false);
    const [showEditMenu, setShowEditMenu] = useState(false);
    const [showCollectionOptions, setShowCollectionOptions] = useState(false);
    //Ref
    const collectionListRef = useRef(null);
    const collectionOptionsRef = useRef(null);
    const colButtonRef = useRef(null);
    const editMenuRef = useRef(null);
    

    //Mouse
    const [mouseX, setMouseX] = useState(0);
    const [mouseY, setMouseY] = useState(0);

    const handleShowRename = () => {
        setShowRenameInput(true);
    };


    

    const handleCollectionOptions = (e) => {
        e.preventDefault();
        setShowCollectionOptions(true);
        setMouseX(e.clientX);
        setMouseY(e.clientY);
    };

    const handleButtonMenu = (e) => {
        e.preventDefault();
        setShowEditMenu(true);
        setMouseX(e.clientX);
        setMouseY(e.clientY);
        
        
    };
    const handleRenameCollection = (e) => {
        setCurrentCollection(e.target.value);
    };
    const handleCollectionKeyDown = (e) => {
        if (e.key === "Enter") {

            setShowRenameInput(false);
            handleCollectionRename();
        }
    };

    const handleTitleChange = (e) => {
        setTitle(e.target.value);
    };
    const handleTitleKeyDown = (e) => {
        if (e.key === "Enter") {

            setEditingTitle(false);
            handleTitleEdit();
        }
    };
    const handleItemClick = (title, body) => {
        setLoadCollection(true);
        setEditorContent((prev) => ({ ...prev, html: body }));
        setTitle(title);
        if (editingTitle)
            setEditingTitle(false);
        
    };

    

    const handleCollectionClick = () => {
        setShowList(!showList);
        
    };

    const handleDeleteItem = () => {
        axios.delete(`http://localhost:5000/delete-item/${itemID}`)
            .then(res => {
                getAllItems();
            })
            .catch(err => console.log(err));
    };

    const handleCollectionRename = () => {
        axios.put(`http://localhost:5000/rename-collection/${currentCollection}`)
            .then(res => toggleRefresh(!refreshCollections))
            .catch(err => console.log(err))
    };
    const handleDeleteCollection = () => {
        axios.delete("http://localhost:5000/delete-collection")
            .then(res => {
                console.log("deleted");
                toggleRefresh(!refreshCollections);
            })
            .catch(err => {console.log(err) })
    };
    const handleCollectionChange = (collection) => {
        setShowList(showList => !showList);
        axios.post("http://localhost:5000/set-collection", {colName : collection})
            .then(res => {
                setLoadCollection(true);
                setCurrentCollection(collection);
                if (res.data.length === 0) {

                    setTitle(" ");
                    setItems([{ title: " ", body: " " }]);
                    setEditorContent((prev) => ({ ...prev, html: " " }));
                }
                else {
                    
                    setItems(res.data);
                    setTitle(res.data[0].title);
                    setEditorContent((prev) => ({ ...prev, html: res.data[0].body }));
                }
                
                
            })
            .catch(err => console.log(err));
    };
    
    const getAllItems = () => {
        axios.get("http://localhost:5000/all-items")
            .then(res => {
                if (res.data.length === 0)
                    setItems([{title: " ", body: " "}]);
                else
                    setItems(res.data);
                })
            .catch(err => console.log(err));
    };
    const handleCreateCollection = () => {
        axios.post("http://localhost:5000/add-collection")
            .then(res => { setCollections(res.data); })
            .catch(err => console.log(err));
    }; 
    const handleNewNote = () => {
        axios.post("http://localhost:5000/add-item-blank")
            .then(res => { getAllItems(); })
            .catch(err => console.log(err));
    };
    const handleBodyEdit = () => {
        axios.put(`http://localhost:5000/edit-itemBody/${itemID}`, {content: editorContent.json})
            .then(res => { console.log("success"); getAllItems(); })
            .catch(err => console.log(err));
    };
    const handleTitleEdit = () => {
        axios.put(`http://localhost:5000/edit-itemTitle/${itemID}`, { content: title })
            .then(res => { console.log("success"); getAllItems(); })
            .catch(err => console.log(err));
    };


    //get the names of all collections in the db
    useEffect(() => {
        axios.get("http://localhost:5000/all-collections")
            .then(res => {
                setCollections(res.data);
                if (res.data.length > 0) {
                    
                    handleCollectionChange(res.data[0]);

                }
            })
            .catch(err => console.log(err));
    }, []); //empty dependency [] means it doesnt run on updates

    //get the names of all collections in the db
    useEffect(() => {
        axios.get("http://localhost:5000/all-collections")
            .then(res => {
                setCollections(res.data);
                if (res.data.length > 0) {
                    setShowList(showList => !showList);
                    handleCollectionChange(res.data[0]);

                }
            })
            .catch(err => console.log(err));
    }, [refreshCollections]); //empty dependency [] means it doesnt run on updates


    useEffect(() => {
        if (loadCol)
            setLoadCollection(false);
    }, [loadCol])
    useEffect(() => {
        console.log("fetched");
        getAllItems();
        
    }, []);
    
    useEffect(() => {
        const handleLeaveContext = (e) => {
            if (e.button === 0) {                
                if (showList && !colButtonRef.current.contains(e.target))
                    setShowList(false);
                if (showEditMenu)
                    setShowEditMenu(false);
                if (showCollectionOptions)
                    setShowCollectionOptions(false);
            }
        };
        document.addEventListener('click', handleLeaveContext);

        //for unmounting
        return () => {
            document.removeEventListener('click', handleLeaveContext);
        }
    }, [showList, showEditMenu, showCollectionOptions])
    

  return (
      <>
          <div>
          <div>
              <div>
                      <button onContextMenu={handleCollectionOptions} ref={colButtonRef} className="collection-button" onClick={handleCollectionClick}>
                      {currentCollection}    
                  </button>
                      <button onClick={handleNewNote}>
                          New Note
                      </button>
                  {showList && (
                      <div ref={collectionListRef}>
                      <ul className="dropdown-menu">
                          {allCollectionNames.map(collection => (
                              <li className="dropdown-item" onClick={() => handleCollectionChange(collection) } key={collection}>
                                  {collection}
                              </li>
                          )) }
                      </ul>
                      </div>
                  )}
              </div>
              <div className="side-bar">
                      {(allItems.length > 0) && allItems.map(item => (
                          <button className="side-button" onContextMenu={(e) => { handleButtonMenu(e); setItemID(item._id) }} onClick={() => { handleItemClick(item.title, item.body); setItemID(item._id); }} key={item._id}>
                          {item.title}
                      </button>
                  )) }
                  
                               
              </div>
          </div>
              <div>
                  {showRenameInput && (<input className="rename-collection" style={{ top: mouseY, left: mouseX }} type="text" value={currentCollection} onChange={handleRenameCollection} onKeyDown={(e) => { handleCollectionKeyDown(e) }}></input>)}
                  {showCollectionOptions && (
                      <div ref={collectionOptionsRef}
                          className="dropdown-menu"
                          style={{
                              width: '175px',
                              top: mouseY,
                              left: mouseX,

                          }}
                      >
                          <ul>
                              <li className="dropdown-item" onClick={() => handleCreateCollection()}>Create New</li>
                              <li className="dropdown-item" onClick={() => handleShowRename()}>Rename</li>
                              <li className="dropdown-item" onClick={() => handleDeleteCollection()}>Delete</li>
                          </ul>
                      </div>
                  ) }
                  {showEditMenu && (
                      <div ref={editMenuRef}
                        className="dropdown-menu"
                          style={{
                              width: '175px',
                              top: mouseY,
                              left: mouseX,
                              
                          }}
                      >
                          <ul>
                              <li className="dropdown-item" onClick={() => handleDeleteItem()}>Delete</li>
                          </ul>
                      </div>
                  ) }
              </div>
              {editingTitle ?
                  (<input className="title-edit" type="text" value={title} onChange={handleTitleChange} onKeyDown={(e) => { handleTitleKeyDown(e) }}>
                  </input>) :
                  (<h1 onClick={() => { setEditingTitle(true) }} className = "title">{ title }</h1>)
              }
             
              <SimpleEditor value={loadCol ? (editorContent.html) : null}  onChange={setEditorContent}>
              </SimpleEditor>
          
          <div className="edit-container">
                  <button onClick={() => { handleBodyEdit();}} className="edit-button">
                Save
                  </button>
                  
              </div>
          </div>
    </>
  )
}


export default App
