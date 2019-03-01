package main

import "fmt"

func quickSort(source []int, l, u int) {
      if l < u {
            m := partition(source, l, u)
            quickSort(source, l, m-1)
            quickSort(source, m, u)
      }
}

func partition(source []int, l, u int) int { //划分
      var (
            pivot = source[l]
            left = l
            right = l+1
      )
      for ;right<u; right++ {
            if source[right] <= pivot {
                  left++
                  source[left], source[right] = source[right], source[left]
            }
      }
      source[l], source[left] = source[left], source[l]
      return left+1
}

func main() {
      s := []int{10, 6, 7, 4, 2, 5,100}
      quickSort(s, 0, len(s))
      fmt.Println(s)
}
