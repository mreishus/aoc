#!/usr/bin/env nodejs

const runme = () => {
  let fs = require('fs')
  let contents = fs.readFileSync('./input.txt', 'utf8')
  let lines = contents.split(/\n/)
  let twoCount = 0
  let threeCount = 0
  for (let line of lines) {
    const hasTwo = hasExactCount(line, 2)
    const hasThree = hasExactCount(line, 3)
    if (hasTwo) { twoCount += 1 }
    if (hasThree) { threeCount += 1 }
  }
  console.log("Checksum: ");
  console.log(twoCount * threeCount + "\n")

  for (let line1 of lines) {
    for (let line2 of lines) {
      if (areLinesOneOff(line1, line2)) {
        return
      }
    }
  }
}

const areLinesOneOff = (a, b) => {
  let differences = 0
  let diff_index = 0
  for (let i = 0; i < a.length; i++) {
    if (a[i] != b[i]) {
      differences += 1
      diff_index = i
    }
  }
  if (differences == 1) {
    console.log('found it!')
    console.log('------------')
    console.log(a)
    console.log(b)
    const inCommon = a.slice(0, diff_index) + a.slice(diff_index + 1)
    console.log(inCommon);
    console.log('------------')
    return true
  }
  return false
}

const hasExactCount = (line, count) => {
  let seen = {}
  for (let char of line) {
    seen[char] = seen[char] != null ? seen[char] + 1 : 1
  }
  return Object.values(seen).some(x => x === count)
}

runme()
