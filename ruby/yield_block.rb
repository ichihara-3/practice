def yield_block(&block)
    yield
end

yield_block {puts 'hello, ruby world'}

yield_block do 
    File.open('test.txt', 'w') do |f|
        f.write('hello, ruby world!!')
    end
end
