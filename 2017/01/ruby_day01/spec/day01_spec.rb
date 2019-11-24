require 'day01'

RSpec.describe Day01, 'all' do
  context 'part1' do
    it 'basic part1 test' do
      cases = [['1122', 3], ['1111', 4], ['1234', 0], ['91212129', 9]]
      cases.each do |c|
        got = Day01.part1(c[0])
        want = c[1]
        expect(got).to eq want
      end
    end
  end

  context 'part2' do
    it 'basic part2 test' do
      cases = [
        ['1212', 6],
        ['1221', 0],
        ['123425', 4],
        ['123123', 12],
        ['12131415', 4]
      ]
      cases.each do |c|
        got = Day01.part2(c[0])
        want = c[1]
        expect(got).to eq want
      end
    end
  end
end
