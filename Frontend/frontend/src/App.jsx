import './App.css'
import { HashRouter as Router, Routes, Route } from 'react-router-dom'
import { Main } from './Pages/Main'
import { Trash } from './Pages/Trash'


function App() {

    

  return (
      <Router>
          <Routes>
              <Route path="/" element={<Main />} />
              <Route path="/trash" element={<Trash/>} />
          </Routes>
    </Router>
  )
}


export default App
