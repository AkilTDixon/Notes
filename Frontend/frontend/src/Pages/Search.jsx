import cog from '@/components/cog-16.png'
import { Link } from 'react-router-dom'
import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import '../App.css'
import { SimpleEditor } from '@/components/tiptap-templates/simple/simple-editor'

export function Search() {
    const [searchResults, setResults] = useState([]);
    const [currentText, setText] = useState("Search documents...")
    const [itemID, setItemID] = useState("");
    const [editorContent, setEditorContent] = useState({ json: {}, html: "", text: "" });

    const handleTextChange = (e) => {
        setText(e.target.value);
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            handleSearchDatabase();
        }
    }
    const handleSearchDatabase = () => {
        axios.get(`http://localhost:5000/search/query-all-collections/${currentText}`)
            .then(res => {
                setResults(res.data)
            })
            .catch (err => console.log(err));
    }
    const handleItemClick = (title, body) => {
        setEditorContent((prev) => ({ ...prev, html: body }));
        
    };
    return (
        <>
            <div>
                <Link style={{ right: '100px', position: 'fixed', fontSize: '25px' }} to="/"><img src={cog}></img>Home</Link>
                <input type="text" value={currentText} onChange={handleTextChange} onKeyDown={(e) => { handleKeyDown(e) }}></input>
            </div>
            <div className="side-bar">
                {(searchResults.length > 0) && searchResults.map(item => (
                    <button className="side-button" onContextMenu={() => {setItemID(item._id) }} onClick={() => { handleItemClick(item.title, item.body); setItemID(item._id); }} key={item._id}>
                        {item.title}
                    </button>
                ))}


            </div>
            <SimpleEditor value={editorContent.html} onChange={setEditorContent}>
            </SimpleEditor>
        </>
    )
}