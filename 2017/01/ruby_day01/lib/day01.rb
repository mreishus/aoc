class Day01
  def self.part1(nums)
    s1 = nums.chars
    s2 = nums.chars.rotate(1)
    count = 0
    s1.zip(s2).each { |pair| count += pair[0].to_i if pair[0] == pair[1] }
    count
  end
end
