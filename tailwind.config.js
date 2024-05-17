/** @type {import('tailwindcss').Config} */
module.exports = {

  content: ["./templates/*.html",
  "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      colors:{
        'colo_dark':'#333533',
        'colo_darker':'#242423',
        'colo_yellow':'#f5cb5c',
        'colo_white':'#e8eddf',
        'colo_grey':'#cfdbd5',
        
      }

    },
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

