import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Home' },
  { to: '/model', label: 'Model' },
  { to: '/about', label: 'About' },
]

function Navbar() {
  return (
    <header className="border-b border-stone-200 bg-stone-50/80 backdrop-blur sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <NavLink to="/" className="flex items-center gap-2 text-green-800 font-semibold text-lg">
          <span aria-hidden="true">🌿</span>
          Sasya
        </NavLink>

        <nav className="flex items-center gap-1">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === '/'}
              className={({ isActive }) =>
                `px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-green-700 text-white'
                    : 'text-stone-600 hover:text-green-800 hover:bg-stone-100'
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  )
}

export default Navbar
