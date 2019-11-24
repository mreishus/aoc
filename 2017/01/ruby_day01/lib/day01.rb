class Day01
  def self.part1(nums)
    rotate_amount = 1
    captcha(nums, rotate_amount)
  end

  def self.part2(nums)
    rotate_amount = nums.size / 2
    captcha(nums, rotate_amount)
  end

  def self.captcha(nums, rotate_amount)
    s1 = nums.chars
    s2 = nums.chars.rotate(rotate_amount)
    count = 0
    s1.zip(s2).each { |pair| count += pair[0].to_i if pair[0] == pair[1] }
    count
  end
end
