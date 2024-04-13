#let wrapper(body) = {
  set page(paper: "us-letter", margin: (x: 0.156in, y: 0.5in))
  set text(font: "IBM Plex Sans", hyphenate: true, lang: "en", size: 10pt)
  show par: set block(above: 0.8em, below: 0.8em)
  show heading: set block(above: 0.8em, below: 0.9em)
  body
}

#let _sticker(content) = box(
  // stroke: 1pt,
  width: 4in,
  height: 2in,
  inset: 1em,
  content
)

#let sticker(content) = _sticker(align(center + horizon, content))

#let dotdotdot = box(width: 1fr, text(fill: gray, repeat("·")))

#let sheet(
  org: "—",
  team: "—",
  number: "—",
  rooms: (exam: "—", awards: "—"),
  students: ()
) = {
  let indiv(student) = _sticker[
    #stack(
      dir: ltr,
      spacing: 1fr,
      align(horizon, text(size: 2em, weight: "bold")[ID: #student.number]),
      align(horizon, image("bmt black.png", height: 1.6em)),
    )

    #line(length: 100%)

    #align(center + horizon)[
      = #student.name

      #text(size: 1.2em)[
        Organization #dotdotdot _#(org)_ \
        Team         #dotdotdot _#(team)_ (ID: #number) \
        Exam Room    #dotdotdot _#(rooms.exam)_ \
        Awards Room  #dotdotdot _#(rooms.awards)_
      ]
    ]
  ]

  let room(content) = sticker[
    #set text(size: 1.4em)
    *#number • #team* \
    _#(org)_
    #line(length: 100%)
    #content
  ]

  grid(
    columns: 1,
    column-gutter: 0.188in,
    ..range(5).map(idx =>
      if idx < students.len() {
        indiv(students.at(idx))
      } else {
        sticker(image("bmt gray.png", height: 4em))
      },
    ),
  )
}

#let sheets(..args) = grid(
  columns: 2,
  column-gutter: 0.188in,
  ..args,
)

// #sheets(
//   sheet(
//     org: "Moor High School",
//     team: "Black",
//     number: "102",
//     rooms: (exam: "Dwinelle 100", awards: "Dwinelle 145"),
//     students: (
//       (name: "Moor Xu", number: "102A"),
//       (name: "Andrew Liu", number: "102B"),
//       (name: "Oliver Ni", number: "102C"),
//       (name: "Brian Su", number: "102D"),
//       (name: "Danielle Murphy", number: "102E"),
//     )
//   ),
//   sheet(
//     org: "Moor High School",
//     team: "Black",
//     number: "102",
//     rooms: (exam: "Dwinelle 100", awards: "Dwinelle 145"),
//     students: (
//       (name: "Danielle Murphy", number: "102E"),
//       (name: "Brian Su", number: "102D"),
//       (name: "Oliver Ni", number: "102C"),
//       (name: "Andrew Liu", number: "102B"),
//       (name: "Moor Xu", number: "102A"),
//     )
//   )
// )



