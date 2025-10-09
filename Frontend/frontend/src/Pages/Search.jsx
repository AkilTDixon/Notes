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
    const [itemIndex, setIndex] = useState(0);
    const [editorContent, setEditorContent] = useState({ json: {}, html: "", text: "" });
    const [itemCollection, setCollection] = useState("");
    const [changeText, setChangeText] = useState(false);


    const updateBody = (index, newBody) => {
        setResults(prev => {
            const li = [...prev];
            const updated = { ...li[index], body: newBody };

            li[index] = updated;
            return li;

        })
    };

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

    const handleBodyEdit = () => {
        if (itemCollection != "") {
            axios.put(`http://localhost:5000/edit-itemBody/${itemID}`, { content: editorContent.json, flat: editorContent.text, destination: itemCollection })
                .then(res => {
                    console.log("success");
                    updateBody(itemIndex, editorContent.json)
                })
                .catch(err => console.log(err));
        }
    };

    const handleItemClick = (title, body) => {
        setChangeText(true);
        setEditorContent((prev) => ({ ...prev, html: body }));
        
    };

    useEffect(() => {
        if (changeText)
            setChangeText(false);
    }, [changeText])

    return (
        <>
            <div>
                <Link style={{ right: '100px', position: 'fixed', fontSize: '25px' }} to="/"><img src={cog}></img>Home</Link>
                <input style={{
                    height: '35px',
                    width: '300px',
                    fontSize: '20px'
                }} type="text" value={currentText} onChange={handleTextChange} onKeyDown={(e) => { handleKeyDown(e) }}></input>
            </div>
            <div className="side-bar">
                {(searchResults.length > 0) && searchResults.map((item, index) => (
                    <button className="side-button" onClick={() => { handleItemClick(item.title, item.body); setItemID(item._id); setCollection(item.collection); setIndex(index); }} key={item._id}>
                        {item.title}
                    </button>
                ))}


            </div>
            <SimpleEditor value={changeText ? editorContent.html : null} onChange={setEditorContent}>
            </SimpleEditor>

            <div className="edit-container">
                <button onClick={() => { handleBodyEdit(); }} className="edit-button">
                    Save
                </button>
            </div>
        </>
    )
}