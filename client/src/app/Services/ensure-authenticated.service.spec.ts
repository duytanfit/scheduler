import { TestBed } from '@angular/core/testing';

import { EnsureAuthenticated } from './ensure-authenticated.service';

describe('EnsureAuthenticatedService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: EnsureAuthenticated = TestBed.get(EnsureAuthenticated);
    expect(service).toBeTruthy();
  });
});
