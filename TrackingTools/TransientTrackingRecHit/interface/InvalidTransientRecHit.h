#ifndef InvalidTransientRecHit_H
#define InvalidTransientRecHit_H


#include "TrackingTools/TransientTrackingRecHit/interface/TransientTrackingRecHit.h"
#include "DataFormats/TrackingRecHit/interface/InvalidTrackingRecHit.h"
#include "TrackingTools/DetLayers/interface/DetLayer.h"

class InvalidTransientRecHit GCC11_FINAL : public TransientTrackingRecHit {
 public:
  typedef TransientTrackingRecHit Base;
  typedef TrackingRecHit::Type Type;
  
  static RecHitPointer build( const GeomDet * geom, Type type=TrackingRecHit::missing, const DetLayer * layer=nullptr) {
    return std::make_shared<InvalidTransientRecHit>( geom, layer, type );
   // return RecHitPointer( new InvalidTransientRecHit( geom, layer, type ));
  }
  

  ~InvalidTransientRecHit();

  const Surface* surface() const {  return  surface_; }
  
  virtual GlobalPoint globalPosition() const;
  virtual GlobalError globalPositionError() const;
  
  virtual float errorGlobalR() const;
  virtual float errorGlobalZ() const;
  virtual float errorGlobalRPhi() const;
  
  virtual const TrackingRecHit * hit() const { return &me; } // this;}
  virtual InvalidTrackingRecHit * cloneHit() const { return me.clone();}
  
  // duplicate of persistent class
  virtual AlgebraicVector parameters() const;
  virtual AlgebraicSymMatrix parametersError() const;
  virtual AlgebraicMatrix projectionMatrix() const;
  virtual int dimension() const;
  
  virtual LocalPoint localPosition() const;
  virtual LocalError localPositionError() const;
  
  virtual std::vector<const TrackingRecHit*> recHits() const;
  virtual std::vector<TrackingRecHit*> recHits();
  
  virtual bool sharesInput( const TrackingRecHit*, SharedInputType) const { return false;}
  
 private:
  
  void throwError() const;
  
 private:
  Surface const * surface_;
  
  // until all clients are migrated...
  InvalidTrackingRecHit me;

public:  
  /// invalid RecHit - has only GeomDet and Type
  InvalidTransientRecHit( const GeomDet* geom, const DetLayer * layer, Type type) :
    Base(geom == nullptr ? DetId(0) : geom->geographicalId(), geom, type), 
    surface_(geom ? &(det()->surface()) : ( layer ?  &(layer->surface()) : nullptr)),
    me( geom, layer, type)
      {}
  
    // hide the clone method for ReferenceCounted. Warning: this method is still 
  // accessible via the bas class TrackingRecHit interface!
  virtual InvalidTransientRecHit* clone() const {return new InvalidTransientRecHit(*this);}

};

#endif
