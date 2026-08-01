function Footer() {
  return (
    <footer className="border-t border-stone-200 bg-stone-50 mt-auto">
      <div className="max-w-4xl mx-auto px-4 py-6 text-sm text-stone-500 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p>
          Treatment data sourced primarily from{' '}
          <a
            href="https://agritech.tnau.ac.in/"
            target="_blank"
            rel="noreferrer"
            className="text-green-700 hover:underline"
          >
            TNAU Agritech Portal
          </a>
          , with model training on{' '}
          <a
            href="https://plantvillage.psu.edu/"
            target="_blank"
            rel="noreferrer"
            className="text-green-700 hover:underline"
          >
            PlantVillage
          </a>{' '}
          and other datasets.
        </p>

        <a
          href="https://github.com/vinithgomez/Sasya"
          target="_blank"
          rel="noreferrer"
          className="text-stone-600 hover:text-green-800 font-medium whitespace-nowrap"
        >
          GitHub ↗
        </a>
      </div>
    </footer>
  )
}

export default Footer
