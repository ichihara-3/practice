#/usr/bin/ruby
# test the number you choose
# whether it is equal to a random num

target = rand(10)

num = 10
while num != target
  puts 'Input a integer in 0-9'
  num = gets.to_i
  if num < target
    puts 'too small'
  elsif num > target
    puts 'too large'
  end
end
puts 'You got a right number!!'
