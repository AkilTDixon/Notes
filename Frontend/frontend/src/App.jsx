import './App.css'
import { HashRouter as Router, Routes, Route } from 'react-router-dom'
import { Main } from './Pages/Main'
import { Trash } from './Pages/Trash'
import { Search } from './Pages/Search'

function App() {

    

  return (
      <Router>
          <Routes>
              <Route path="/" element={<Main />} />
              <Route path="/trash" element={<Trash />} />
              <Route path="/search" element={<Search />} />
          </Routes>
    </Router>
  )
}


export default App
