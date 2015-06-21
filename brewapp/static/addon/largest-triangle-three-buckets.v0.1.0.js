/*! largest-triangle-three-buckets - v0.1.0 - 2014-12-07
* Copyright (c) 2014 Josh Carr; Licensed MIT */
// Uses AMD or browser globals to create a module.

// Grabbed from https://github.com/umdjs/umd/blob/master/amdWeb.js.
// Check out https://github.com/umdjs/umd for more patterns.

// Defines a module "largest-triangle-three-buckets".
// Note that the name of the module is implied by the file name. It is best
// if the file name and the exported global have matching names.

// If you do not want to support the browser global path, then you
// can remove the `root` use and the passing `this` as the first arg to
// the top function.

(function (root, factory) {
  'use strict';
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define([], factory);
  } else {
    // Browser globals
    root.largestTriangleThreeBuckets = factory();
  }
}(this, function () {
  'use strict';

  /*** YOUR LIBRARY CODE GOES HERE! ***/

  function largestTriangleThreeBuckets(data, threshold, xAccessor, yAccessor) {

    var floor = Math.floor,
      abs = Math.abs;

    var daraLength = data.length;
    if (threshold >= daraLength || threshold === 0) {
      return data; // Nothing to do
    }

    var sampled = [],
      sampledIndex = 0;

    // Bucket size. Leave room for start and end data points
    var every = (daraLength - 2) / (threshold - 2);

    var a = 0,  // Initially a is the first point in the triangle
      maxAreaPoint,
      maxArea,
      area,
      nextA;

    sampled[ sampledIndex++ ] = data[ a ]; // Always add the first point

    for (var i = 0; i < threshold - 2; i++) {

      // Calculate point average for next bucket (containing c)
      var avgX = 0,
        avgY = 0,
        avgRangeStart  = floor( ( i + 1 ) * every ) + 1,
        avgRangeEnd    = floor( ( i + 2 ) * every ) + 1;
      avgRangeEnd = avgRangeEnd < daraLength ? avgRangeEnd : daraLength;

      var avgRangeLength = avgRangeEnd - avgRangeStart;

      for ( ; avgRangeStart<avgRangeEnd; avgRangeStart++ ) {
        avgX += data[ avgRangeStart ][ xAccessor ] * 1; // * 1 enforces Number (value may be Date)
        avgY += data[ avgRangeStart ][ yAccessor ] * 1;
      }
      avgX /= avgRangeLength;
      avgY /= avgRangeLength;

      // Get the range for this bucket
      var rangeOffs = floor( (i + 0) * every ) + 1,
        rangeTo   = floor( (i + 1) * every ) + 1;

      // Point a
      var pointAX = data[ a ][ xAccessor ] * 1, // enforce Number (value may be Date)
        pointAY = data[ a ][ yAccessor ] * 1;

      maxArea = area = -1;

      for ( ; rangeOffs < rangeTo; rangeOffs++ ) {
        // Calculate triangle area over three buckets
        area = abs( ( pointAX - avgX ) * ( data[ rangeOffs ][ yAccessor ] - pointAY ) -
              ( pointAX - data[ rangeOffs ][ xAccessor ] ) * ( avgY - pointAY )
              ) * 0.5;
        if ( area > maxArea ) {
          maxArea = area;
          maxAreaPoint = data[ rangeOffs ];
          nextA = rangeOffs; // Next a is this b
        }
      }

      sampled[ sampledIndex++ ] = maxAreaPoint; // Pick this point from the bucket
      a = nextA; // This a is the next a (chosen b)
    }

    sampled[ sampledIndex++ ] = data[ daraLength - 1 ]; // Always add last

    return sampled;
  }

  // Return a value to define the module export.
  // This example returns a functions, but the module
  // can return an object as the exported value.
  return largestTriangleThreeBuckets;
}));
