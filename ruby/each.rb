
array1 = Array((1..17))
array2 = [2,4,6,8]
target = [array1, array2]

# 1. only using "each"
line = ''
target.each do |i|
    i.each {|num| line = line + num.to_s + ' '}
end
puts line

# 2. using "each_slice"
target.each_slice(2) do |arr|
   puts arr[0].join(" ") + " " + arr[1].join(" ") 
end
