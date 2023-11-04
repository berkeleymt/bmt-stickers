#let _sticker(content) = box(
  // stroke: 1pt,
  width: 4in,
  height: 2in,
  inset: 1em,
  content
)

#let sticker(content) = _sticker(align(center + horizon, content))

#let sheet(
  org: "-",
  team: "-",
  number: "-",
  rooms: (power: "-", guts: "-", awards: "-"),
  students: ()
) = {
  set page(paper: "us-letter", margin: (x: 0.156in, y: 0.5in))
  set text(hyphenate: true, lang: "en")
  show par: set block(above: 1em, below: 1em)
  show heading: set block(above: 1em, below: 1em)

  let indiv(student) = _sticker[
    #stack(
      dir: ltr,
      spacing: 1fr,
      align(bottom, text(size: 2.5em, weight: "bold", student.number)),
      align(bottom, image("bmt black.png", height: 2em)),
    )

    #line(length: 100%)

    #align(center + horizon)[
      = #student.name

      #text(size: 1.2em)[
        _#(org)_ \
        _#number • #(team)_
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
    columns: 2,
    column-gutter: 0.188in,
    ..students.map(student => indiv(student)),
    ..range(students.len(), 6).map(_ => sticker(image("bmt gray.png", height: 4em))),
    room[
      *Power Room* \
      #rooms.power
    ],
    room[
      *Guts Room* \
      #rooms.guts
    ],
    room[
      *Awards Room* \
      #rooms.awards
    ],
    sticker[
      *#number • #team* \
      _#(org)_

      #table(
        columns: (1fr, 1.4fr, 2.4fr),
        [*Time*], [*Event*], [*Room Assignment* ],
        [9:00 AM], [Power Round], rooms.power,
        [10:45 AM], [Focus Rounds], [_Check Tournament Guide_],
        [4:00 PM], [Guts Round], rooms.guts,
        [6:00 PM], [Awards], rooms.awards,
      )
    ],
  )
}
